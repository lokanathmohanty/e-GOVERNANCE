from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates initial test users for the application'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        users = [
            {
                'username': 'admin',
                'password': 'Password@123',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            },
            {
                'username': 'final_tester',
                'password': 'Password@123',
                'role': 'citizen',
                'is_staff': False,
                'is_superuser': False,
                'email': 'tester@example.com'
            },
            {
                'username': 'officer1',
                'password': 'Password@123',
                'role': 'officer',
                'is_staff': True,  # Officers might need staff access depending on your setup
                'is_superuser': False,
                'email': 'officer1@example.com'
            },
            {
                'username': 'head1',
                'password': 'Password@123',
                'role': 'department_head',
                'is_staff': True,  # Heads usually need staff access
                'is_superuser': False,
                'email': 'head1@example.com'
            }
        ]

        for user_data in users:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                self.stdout.write(f'Creating user: {username} ({user_data["role"]})')
                if user_data['is_superuser']:
                    user = User.objects.create_superuser(
                        username=username,
                        email=user_data['email'],
                        password=user_data['password'],
                        role=user_data['role']
                    )
                else:
                    # Create user and set attributes manually to ensure correctness
                    user = User(
                        username=username,
                        email=user_data['email'],
                        role=user_data['role'],
                        is_staff=user_data['is_staff']
                    )
                    user.set_password(user_data['password'])
                    user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
