from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as django_settings
from .models import (
    Subject, UserProgress, Question, UserProfile, Flashcard, 
    VocationalSkill, BroadcastMessage, LearningCategory, LearningTopic, LearningProgress
)
import google.generativeai as genai
import json
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from datetime import timedelta, datetime

# ================== AI CHAT WITH GEMINI ==================
@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            # Configure Gemini
            api_key = django_settings.GEMINI_API_KEY
            if not api_key:
                return JsonResponse({'reply': "Hi! The AI is ready, but you need to add the 'GEMINI_API_KEY' to your Render Environment variables first!"})

            genai.configure(api_key=api_key)
            
            # Support both JSON and multipart/form-data (for file uploads)
            if request.content_type and 'multipart/form-data' in request.content_type:
                user_message = request.POST.get('message', '')
                language = request.POST.get('language', 'English')
                uploaded_file = request.FILES.get('file', None)
            else:
                data = json.loads(request.body)
                user_message = data.get('message', '')
                language = data.get('language', 'English')
                uploaded_file = None

            # Strong language enforcement
            lang_map = {
                'Hausa': 'Hausa (Harshen Hausa)',
                'Yoruba': 'Yoruba (Èdè Yorùbá)',
                'Igbo': 'Igbo (Asụsụ Igbo)',
                'French': 'French (Français)',
                'Arabic': 'Arabic (اللغة العربية)',
                'English': 'English',
            }
            lang_full = lang_map.get(language, language)

            system_prompt = f"""STRICT INSTRUCTION: You MUST reply ONLY in {lang_full}. Do NOT use English unless {lang_full} is English. Every single word in your response must be in {lang_full}.

You are QualiLearn AI, a friendly tutor for Nigerian students studying for JAMB and WAEC.
Be clear, encouraging, and give step-by-step explanations.
If the student uploads an image or document, analyze it carefully.

Remember: RESPOND ONLY IN {lang_full}."""

            # Build content parts for multimodal input
            content_parts = [system_prompt + f"\n\nStudent: {user_message}"]

            if uploaded_file:
                import PIL.Image
                import io
                file_bytes = uploaded_file.read()
                file_type = uploaded_file.content_type

                if 'image' in file_type:
                    # Send image directly to Gemini
                    image = PIL.Image.open(io.BytesIO(file_bytes))
                    content_parts = [
                        system_prompt + f"\n\nThe student has uploaded an image and says: '{user_message}'. Please analyze the image and respond helpfully.",
                        image
                    ]
                elif 'pdf' in file_type:
                    # For PDFs, extract text or send as bytes
                    content_parts = [
                        system_prompt + f"\n\nThe student has uploaded a PDF document and says: '{user_message}'. The file data is attached.",
                        {"mime_type": "application/pdf", "data": file_bytes}
                    ]

            # Try multiple model names for best compatibility
            model_names = [
                'gemini-3-flash-preview',
                'gemini-3.0-flash-preview',
                'gemini-2.0-flash-exp',
                'gemini-1.5-flash', 
                'gemini-pro'
            ]
            
            last_error = None
            response = None
            
            for name in model_names:
                try:
                    model = genai.GenerativeModel(name)
                    response = model.generate_content(content_parts)
                    break # Success!
                except Exception as e:
                    last_error = e
                    continue
            
            if not response:
                return JsonResponse({'reply': f"AI Error: All models failed. Last Error: {str(last_error)}"})

            ai_reply = response.text
            return JsonResponse({'reply': ai_reply})

        except Exception as e:
            print("Gemini Error:", str(e))
            error_msg = str(e)
            return JsonResponse({'reply': f"AI Error Detail: {error_msg}"})

        finally:
            # Increment study time for AI Chat interaction
            if request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                profile.total_study_minutes += 2
                profile.save()

    return JsonResponse({'reply': 'Hello! How can I help you today?'})


# ================== AUTHENTICATION ==================
def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# ================== MAIN VIEWS ==================
def home(request):
    return render(request, 'index.html')

def chat(request):
    return render(request, 'chat.html')

@login_required
def dashboard(request):
    progress = UserProgress.objects.filter(user=request.user).order_by('-last_attempt')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    today = timezone.localtime().date()
    
    # Update streak
    if profile.last_active_date != today:
        if profile.last_active_date == today - timedelta(days=1):
            profile.streak_count += 1
        else:
            profile.streak_count = 1
        profile.last_active_date = today
        profile.save()
        
    streak_word = "on fire \u2014 keep it going!"
    if profile.streak_count == 1:
        streak_word = "just sparking \u2014 keep building it!"
    elif profile.streak_count >= 5:
        streak_word = "absolutely legendary!"
        
    hours = profile.total_study_minutes // 60
    minutes = profile.total_study_minutes % 60
    study_time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    
    # Average score
    total_score = 0
    total_q = 0
    for p in progress:
        total_score += p.score
        total_q += p.total_questions
    average_score = round((total_score / total_q) * 100) if total_q > 0 else 0

    # Notifications (Broadcast Messages)
    notifications = BroadcastMessage.objects.all().order_by('-created_at')[:5]
    notification_count = notifications.count()

    # Count assessments passed (count of UserProgress where score > 0)
    assessments_passed = progress.filter(score__gte=1).count()

    return render(request, 'dashboard.html', {
        'progress': progress,
        'profile': profile,
        'streak_word': streak_word,
        'study_time_str': study_time_str,
        'average_score': average_score,
        'notifications': notifications,
        'notification_count': notification_count,
        'assessments_passed': assessments_passed
    })

@login_required
def assessment(request):
    # Fetch subjects with their question counts
    subjects_list = Subject.objects.all()
    subjects = []
    for s in subjects_list:
        subjects.append({
            'id': s.id,
            'name': s.name,
            'q_count': Question.objects.filter(subject=s).count()
        })
    
    progress_history = UserProgress.objects.filter(user=request.user).order_by('-last_attempt')
    
    recent_score = request.session.pop('recent_score', None)
    recent_total = request.session.pop('recent_total', None)
    
    return render(request, 'assessment.html', {
        'subjects': subjects,
        'progress_history': progress_history,
        'recent_score': recent_score,
        'recent_total': recent_total
    })

@login_required
def start_assessment(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        
        try:
            subject = Subject.objects.get(id=subject_id)
        except:
            return redirect('assessment')
        
        # Fetch from our new database implementation (all questions for the subject)
        db_questions = Question.objects.filter(subject=subject).order_by('?')
        
        if not db_questions.exists():
            messages.warning(request, f"The subject '{subject.name}' has no questions uploaded yet. Please contact the admin.")
            return redirect('assessment')

        questions = []
        option_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        for q in db_questions:
            questions.append({
                "id": q.id,
                "text": q.text,
                "options": [q.option_a, q.option_b, q.option_c, q.option_d],
                "correct": option_map.get(str(q.correct_option).lower().strip(), 0)
            })
            
        request.session['current_questions'] = questions
        request.session['current_subject_id'] = subject.id
        request.session['time_limit'] = len(questions) * 30 # 30 seconds per question
        request.session['assessment_start_time'] = timezone.now().isoformat()
        return redirect('take_assessment')
    return redirect('assessment')

@login_required
def take_assessment(request):
    questions = request.session.get('current_questions')
    time_limit = request.session.get('time_limit', 900)
    if not questions:
        return redirect('assessment')
    return render(request, 'take_assessment.html', {'questions': questions, 'time_limit': time_limit})

@login_required
def submit_assessment(request):
    if request.method == 'POST':
        questions = request.session.get('current_questions')
        if not questions:
            return redirect('dashboard')
        score = 0
        for q in questions:
            answer = request.POST.get(f'q_{q["id"]}')
            if answer and int(answer) == q["correct"]:
                score += 1
        subject = Subject.objects.get(id=request.session.get('current_subject_id'))
        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            subject=subject,
            defaults={'total_questions': len(questions), 'score': score}
        )
        
        # Update progress tracking
        if score >= progress.score:
            progress.score = score
        progress.total_questions = len(questions)
        
        if progress.percentage() >= 50:
            progress.completed = True
            
        progress.last_attempt = timezone.now()
        progress.save()
        
        # Add study time (calculated from actual time elapsed)
        start_time_str = request.session.get('assessment_start_time')
        if start_time_str:
            try:
                start_time = datetime.fromisoformat(start_time_str)
                # Ensure start_time is timezone-aware if the current time is
                if timezone.is_aware(timezone.now()) and not timezone.is_aware(start_time):
                    start_time = timezone.make_aware(start_time)
                elapsed = timezone.now() - start_time
                minutes_to_add = max(1, round(elapsed.total_seconds() / 60))
            except:
                minutes_to_add = len(questions) * 2
        else:
            # Fallback to questions count if start_time is missing
            minutes_to_add = len(questions) * 2

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_study_minutes += minutes_to_add
        profile.save()
        
        request.session['recent_score'] = score
        request.session['recent_total'] = len(questions)
        
        for key in ['current_questions', 'current_subject_id', 'time_limit', 'assessment_start_time']:
            request.session.pop(key, None)
        return redirect('assessment')
    return redirect('assessment')

@login_required
def learning(request):
    # Subjects are the real top-level items (each Subject has learning_topics)
    subjects = Subject.objects.select_related('category').prefetch_related('learning_topics').order_by('category__order', 'name')

    # Get user progress
    user_progress = LearningProgress.objects.filter(user=request.user, is_completed=True).values_list('topic_id', flat=True)
    user_progress_set = set(user_progress)

    # Calculate overall progress
    total_topics = LearningTopic.objects.count()
    completed_count = len(user_progress_set)
    overall_percentage = round((completed_count / total_topics) * 100) if total_topics > 0 else 0

    # Build syllabus list — one entry per Subject, topics inside
    syllabus = []
    for subj in subjects:
        subj_topics = []
        subj_completed = 0

        for t in subj.learning_topics.all():
            is_done = t.id in user_progress_set
            if is_done:
                subj_completed += 1
            # Use stored YouTube URL if available, fall back to a search link
            yt_url = t.youtube_url if t.youtube_url else (
                f"https://www.youtube.com/results?search_query="
                f"{subj.name.replace(' ', '+')}+{t.name.replace(' ', '+')}+JAMB+WAEC+tutorial"
            )
            subj_topics.append({
                'id': t.id,
                'name': t.name,
                'is_completed': is_done,
                'youtube_url': yt_url,
            })

        subj_total = len(subj_topics)
        syllabus.append({
            'id': subj.id,
            'name': subj.name,
            'icon': subj.category.icon_class if subj.category else 'bi-book',
            'topics': subj_topics,
            'completed_count': subj_completed,
            'total_count': subj_total,
            'percentage': round((subj_completed / subj_total) * 100) if subj_total > 0 else 0,
        })

    return render(request, 'learning.html', {
        'syllabus': syllabus,
        'overall_percentage': overall_percentage,
        'completed_count': completed_count,
        'total_topics': total_topics,
    })

@csrf_exempt
@login_required
def toggle_learning_completion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic_id = data.get('topic_id')
            is_completed = data.get('is_completed', False)
            
            topic = LearningTopic.objects.get(id=topic_id)
            progress, created = LearningProgress.objects.get_or_create(
                user=request.user,
                topic=topic
            )
            progress.is_completed = is_completed
            if is_completed:
                progress.completed_at = timezone.now()
            else:
                progress.completed_at = None
            progress.save()
            
            # Recalculate stats for response
            user_completed = LearningProgress.objects.filter(user=request.user, is_completed=True).count()
            total_topics = LearningTopic.objects.count()
            overall_percentage = round((user_completed / total_topics) * 100) if total_topics > 0 else 0
            
            return JsonResponse({
                'status': 'success',
                'overall_percentage': overall_percentage,
                'completed_count': user_completed
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
@login_required
def flashcard(request):
    subjects_list = Subject.objects.all()
    subjects = []
    for s in subjects_list:
        subjects.append({
            'id': s.id,
            'name': s.name,
            'fc_count': Flashcard.objects.filter(subject=s).count()
        })
    return render(request, 'flashcard.html', {'subjects': subjects})

@login_required
def start_flashcard(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        
        try:
            subject = Subject.objects.get(id=subject_id)
        except:
            return redirect('flashcard')
        
        db_flashcards = Flashcard.objects.filter(subject=subject).order_by('?')
        
        if not db_flashcards.exists():
            messages.warning(request, f"The subject '{subject.name}' has no flashcards uploaded yet. Please contact the admin.")
            return redirect('flashcard')

        flashcards = []
        for f in db_flashcards:
            flashcards.append({
                "id": f.id,
                "front": f.front,
                "back": f.back
            })
            
        request.session['current_flashcards'] = flashcards
        request.session['current_fc_subject_id'] = subject.id
        request.session['current_fc_subject_name'] = subject.name

        # Increment study time for Flashcard session
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_study_minutes += 5
        profile.save()

        return redirect('take_flashcard')
    return redirect('flashcard')

@login_required
def take_flashcard(request):
    flashcards = request.session.get('current_flashcards')
    subject_name = request.session.get('current_fc_subject_name', 'Subject')
    if not flashcards:
        return redirect('flashcard')
    
    # We pass the list to the template, it will be handled by JavaScript
    return render(request, 'take_flashcard.html', {
        'flashcards_json': json.dumps(flashcards),
        'subject_name': subject_name,
        'total_cards': len(flashcards)
    })
def games(request): return render(request, 'games.html')
@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        return redirect('profile')
        
    all_progress = UserProgress.objects.filter(user=request.user)
    total_percentage = 0
    completed_courses = []
    assessments_passed = 0

    for p in all_progress:
        perc = p.percentage()
        total_percentage += perc
        if p.completed:
            assessments_passed += 1
            completed_courses.append(p)
    
    overall_progress = round(total_percentage / len(all_progress)) if all_progress else 0
    total_study_hours = user_profile.total_study_minutes // 60
    
    context = {
        'profile': user_profile,
        'overall_progress': overall_progress,
        'total_study_hours': total_study_hours,
        'assessments_passed': assessments_passed,
        'completed_courses': completed_courses
    }
    return render(request, 'profile.html', context)
@login_required
def settings(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            return redirect('settings')
        elif 'update_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if request.user.check_password(current_password):
                if new_password and new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
            return redirect('settings')
            
    return render(request, 'settings.html')
@login_required
def vocational(request):
    practical_skills = VocationalSkill.objects.filter(category='Practical Skills')
    soft_skills = VocationalSkill.objects.filter(category='Soft / Digital Skills')
    return render(request, 'vocational.html', {
        'practical_skills': practical_skills,
        'soft_skills': soft_skills
    })

@login_required
def setup_admin(request):
    """Temporary view to promote a user to superuser status."""
    # Only allow if the secret key is provided in the URL
    if request.GET.get('key') == 'qualilearn_admin_2024':
        user = request.user
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return JsonResponse({
            'status': 'Success', 
            'message': f'User {user.username} is now an Admin! You can now visit /admin/ to manage the site.'
        })
    return JsonResponse({'status': 'Error', 'message': 'Invalid secret key.'}, status=403)



    if request.GET.get('key') == 'qualilearn_admin_2024':
        user = request.user
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return JsonResponse({
            'status': 'Success', 
            'message': f'User {user.username} is now an Admin! You can now visit /admin/ to manage the site.'
        })
    return JsonResponse({'status': 'Error', 'message': 'Invalid secret key.'}, status=403)