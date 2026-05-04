from django.core.management.base import BaseCommand
from core.models import LearningCategory, Subject, LearningTopic


class Command(BaseCommand):
    help = 'Seeds the database with JAMB/WAEC subjects and topics with YouTube links'

    def handle(self, *args, **options):
        self.stdout.write('Seeding learning data...')

        # Create the main category
        cat, _ = LearningCategory.objects.get_or_create(
            name='JAMB / WAEC Syllabus',
            defaults={'icon_class': 'bi-journal-bookmark-fill', 'order': 1}
        )

        DATA = {
            'Mathematics': [
                ('Number & Numeration', 'https://www.youtube.com/watch?v=VBVKNcGPpgA'),
                ('Fractions, Decimals & Percentages', 'https://www.youtube.com/watch?v=2aOjPM4ePgA'),
                ('Ratio, Proportion & Rates', 'https://www.youtube.com/watch?v=USmit5zUGas'),
                ('Algebraic Expressions', 'https://www.youtube.com/watch?v=Qyd_v3DGzTM'),
                ('Linear & Quadratic Equations', 'https://www.youtube.com/watch?v=IWigU4wFpnA'),
                ('Inequalities', 'https://www.youtube.com/watch?v=xUEB4eTYBLQ'),
                ('Indices, Logarithms & Surds', 'https://www.youtube.com/watch?v=ntBWrcbAhaY'),
                ('Sequences & Series', 'https://www.youtube.com/watch?v=pXo0bG4iAyg'),
                ('Variation', 'https://www.youtube.com/watch?v=T_p0P5B0X54'),
                ('Trigonometry', 'https://www.youtube.com/watch?v=PUB0TaZ7bhA'),
                ('Geometry (Plane & Solid)', 'https://www.youtube.com/watch?v=302eJ3TzJQU'),
                ('Coordinate Geometry', 'https://www.youtube.com/watch?v=9Kc_1jbOD2E'),
                ('Mensuration', 'https://www.youtube.com/watch?v=I_7MOAQG5BA'),
                ('Statistics', 'https://www.youtube.com/watch?v=xxpc-HPKN28'),
                ('Probability', 'https://www.youtube.com/watch?v=uzkc-qNVoOk'),
            ],
            'English Language': [
                ('Comprehension', 'https://www.youtube.com/watch?v=WVi0sDc1qlQ'),
                ('Summary Writing', 'https://www.youtube.com/watch?v=e5MzSFLI8vY'),
                ('Essay Writing (Narrative, Descriptive, Argumentative, Expository)', 'https://www.youtube.com/watch?v=QYJ1C28LXkY'),
                ('Lexis & Structure', 'https://www.youtube.com/watch?v=2hVAcEJh_8I'),
                ('Parts of Speech', 'https://www.youtube.com/watch?v=SceDmiBEFYo'),
                ('Tenses', 'https://www.youtube.com/watch?v=VrpSS1hUR90'),
                ('Concord', 'https://www.youtube.com/watch?v=GzFv0yDJkVE'),
                ('Idioms & Proverbs', 'https://www.youtube.com/watch?v=8_MXcnGbWiQ'),
                ('Registers', 'https://www.youtube.com/watch?v=hLmEJaM-5yM'),
                ('Oral English (Phonetics, Stress, Intonation)', 'https://www.youtube.com/watch?v=SMAQJo25JEs'),
            ],
            'Physics': [
                ('Measurements & Units', 'https://www.youtube.com/watch?v=qDGnjScNM_g'),
                ('Scalars & Vectors', 'https://www.youtube.com/watch?v=WNuIhXo39_k'),
                ('Motion (Kinematics)', 'https://www.youtube.com/watch?v=ZM8ECpBuQYE'),
                ('Forces & Laws of Motion', 'https://www.youtube.com/watch?v=kKKM8Y-u7ds'),
                ('Work, Energy & Power', 'https://www.youtube.com/watch?v=w4QFJb9a8vo'),
                ('Machines', 'https://www.youtube.com/watch?v=DqeMQDgiY-I'),
                ('Heat & Temperature', 'https://www.youtube.com/watch?v=vqDbMEdLiCs'),
                ('Waves (Sound & Light)', 'https://www.youtube.com/watch?v=Rbuhdo0AZDU'),
                ('Optics', 'https://www.youtube.com/watch?v=Oh4m8Ees-3Q'),
                ('Electricity', 'https://www.youtube.com/watch?v=mc979OhitAg'),
                ('Magnetism', 'https://www.youtube.com/watch?v=snNG481SYJo'),
                ('Electromagnetism', 'https://www.youtube.com/watch?v=rLNM_zIcJCU'),
                ('Atomic & Nuclear Physics', 'https://www.youtube.com/watch?v=cWMJpjlMArE'),
            ],
            'Chemistry': [
                ('Particulate Nature of Matter', 'https://www.youtube.com/watch?v=VDiskGxpP7o'),
                ('Atomic Structure', 'https://www.youtube.com/watch?v=LhveTGblGHY'),
                ('Periodic Table', 'https://www.youtube.com/watch?v=0RRVV4Diomg'),
                ('Chemical Bonding', 'https://www.youtube.com/watch?v=CGA8sRwqIFg'),
                ('Formulae & Stoichiometry', 'https://www.youtube.com/watch?v=UL1jmJaUkaQ'),
                ('States of Matter', 'https://www.youtube.com/watch?v=s-KvoVzukHo'),
                ('Energy Changes', 'https://www.youtube.com/watch?v=GqtUWyDR1fg'),
                ('Rates of Reaction', 'https://www.youtube.com/watch?v=OttRV5ykP7A'),
                ('Chemical Equilibrium', 'https://www.youtube.com/watch?v=dUMmoPdwBy4'),
                ('Acids, Bases & Salts', 'https://www.youtube.com/watch?v=vt8fB3MFzLk'),
                ('Redox Reactions', 'https://www.youtube.com/watch?v=5rtJdras7UI'),
                ('Electrolysis', 'https://www.youtube.com/watch?v=Ql7_EbaRkdo'),
                ('Organic Chemistry', 'https://www.youtube.com/watch?v=bka20Q9TN6M'),
                ('Environmental Chemistry', 'https://www.youtube.com/watch?v=e6rglsLy1Ys'),
            ],
            'Biology': [
                ('Cell Structure & Organization', 'https://www.youtube.com/watch?v=URUJD5NEXC8'),
                ('Classification of Living Things', 'https://www.youtube.com/watch?v=SA02un37GFQ'),
                ('Ecology', 'https://www.youtube.com/watch?v=izRvPaAWgyw'),
                ('Nutrition', 'https://www.youtube.com/watch?v=H8WJ2KENlK0'),
                ('Transport Systems', 'https://www.youtube.com/watch?v=PgI80Ue-AMo'),
                ('Respiration', 'https://www.youtube.com/watch?v=eJ9Zjc-jdys'),
                ('Excretion', 'https://www.youtube.com/watch?v=aQZaNXKyPS4'),
                ('Reproduction', 'https://www.youtube.com/watch?v=_5OvgQW6FG4'),
                ('Growth & Development', 'https://www.youtube.com/watch?v=sEKB7pi1mbc'),
                ('Coordination & Control (Nervous & Hormonal)', 'https://www.youtube.com/watch?v=x4PPZCLnVkA'),
                ('Genetics & Heredity', 'https://www.youtube.com/watch?v=CBezq1fFUEA'),
                ('Evolution', 'https://www.youtube.com/watch?v=GhHOjC4oxh8'),
            ],
            'Economics': [
                ('Basic Economic Concepts', 'https://www.youtube.com/watch?v=3ez10ADR_gM'),
                ('Demand & Supply', 'https://www.youtube.com/watch?v=g9aDizJpd_s'),
                ('Elasticity', 'https://www.youtube.com/watch?v=HHcblIxiAAk'),
                ('Consumer Behavior', 'https://www.youtube.com/watch?v=nOo_p_XGqp4'),
                ('Production', 'https://www.youtube.com/watch?v=P4yDN0MU_jY'),
                ('Cost & Revenue', 'https://www.youtube.com/watch?v=5hLnBEVPFGQ'),
                ('Market Structures', 'https://www.youtube.com/watch?v=k-ysLFVLfto'),
                ('Distribution of Income', 'https://www.youtube.com/watch?v=PHe0bXAIuk0'),
                ('National Income', 'https://www.youtube.com/watch?v=m78hko2tOeM'),
                ('Money & Banking', 'https://www.youtube.com/watch?v=fTTGALaRZoc'),
                ('Inflation & Deflation', 'https://www.youtube.com/watch?v=T8-85cZRI9o'),
                ('Public Finance', 'https://www.youtube.com/watch?v=GJ4TTNeSUdQ'),
                ('International Trade', 'https://www.youtube.com/watch?v=LsOqKkfR4bA'),
                ('Economic Development & Planning', 'https://www.youtube.com/watch?v=QSlIGxYyC94'),
            ],
            'Government': [
                ('Meaning & Scope of Government', 'https://www.youtube.com/watch?v=Kl4-7OsWl0E'),
                ('Forms of Government', 'https://www.youtube.com/watch?v=Ggz_gd--UO0'),
                ('Systems of Government', 'https://www.youtube.com/watch?v=gD_VJ4BEDu0'),
                ('Constitution', 'https://www.youtube.com/watch?v=BzHOaEDNmOU'),
                ('Rule of Law', 'https://www.youtube.com/watch?v=AOx3ElMkxnk'),
                ('Separation of Powers', 'https://www.youtube.com/watch?v=pDfBx3ULPGQ'),
                ('Citizenship', 'https://www.youtube.com/watch?v=hAF0E4DhyBc'),
                ('Political Parties', 'https://www.youtube.com/watch?v=IjjZMhGdnSo'),
                ('Pressure Groups', 'https://www.youtube.com/watch?v=wgT0v3F9lvU'),
                ('Electoral Process', 'https://www.youtube.com/watch?v=HaJQC8DhGOA'),
                ('Public Administration', 'https://www.youtube.com/watch?v=7eswTiUHuOA'),
                ('Local Government', 'https://www.youtube.com/watch?v=3gKqNGxoKRA'),
                ('Nigerian Government & Politics', 'https://www.youtube.com/watch?v=xjS25m-P5X4'),
                ('International Relations', 'https://www.youtube.com/watch?v=JJ-CUMJcORE'),
            ],
            'Geography': [
                ('Map Reading & Interpretation', 'https://www.youtube.com/watch?v=aA3BjPGh-LY'),
                ('Earth Structure', 'https://www.youtube.com/watch?v=eXiVGEEPQ6c'),
                ('Rocks & Minerals', 'https://www.youtube.com/watch?v=bTFv8SIddhM'),
                ('Landforms', 'https://www.youtube.com/watch?v=RD_OuYAnGqU'),
                ('Weather & Climate', 'https://www.youtube.com/watch?v=vH298zSCQzY'),
                ('Vegetation', 'https://www.youtube.com/watch?v=w77zPAtVTuI'),
                ('Soil', 'https://www.youtube.com/watch?v=8-Fkx1GNO9g'),
                ('Environmental Resources', 'https://www.youtube.com/watch?v=NW-1oNeA4rA'),
                ('Population', 'https://www.youtube.com/watch?v=E8dkWQVFAoA'),
                ('Settlement', 'https://www.youtube.com/watch?v=H7lw-x6DIAS'),
                ('Transportation', 'https://www.youtube.com/watch?v=NvMseOBBN9E'),
                ('Trade', 'https://www.youtube.com/watch?v=NI9TLDIPVcs'),
                ('Industries', 'https://www.youtube.com/watch?v=5k7FPlVJqtw'),
                ('Regional Geography (Nigeria & Africa)', 'https://www.youtube.com/watch?v=hkbLxP99qb4'),
            ],
        }

        total_subjects = 0
        total_topics = 0

        for subject_name, topics in DATA.items():
            subj, _ = Subject.objects.get_or_create(
                name=subject_name,
                defaults={'category': cat}
            )
            # Link to category if not already
            if not subj.category:
                subj.category = cat
                subj.save()
            total_subjects += 1

            for order, (topic_name, yt_url) in enumerate(topics, start=1):
                _, created = LearningTopic.objects.get_or_create(
                    subject=subj,
                    name=topic_name,
                    defaults={'youtube_url': yt_url, 'order': order}
                )
                if created:
                    total_topics += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {total_subjects} subjects and {total_topics} topics!'
        ))
