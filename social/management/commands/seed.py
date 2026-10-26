from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from social.models import Profile, Post, Follow
class Command(BaseCommand):
    help = "Create demo users (password: demo12345) and posts"
    def handle(self, *a, **k):
        users = []
        for n, bio, t in [("ada", "Maths and machines.", "Just wrote my first program."),
                          ("grace", "Debugging since 1947.", "Found a literal bug in the hardware today."),
                          ("linus", "Kernel person.", "Talk is cheap. Show me the code.")]:
            u, new = User.objects.get_or_create(username=n)
            if new: u.set_password("demo12345"); u.save(); Post.objects.create(author=u, text=t)
            Profile.objects.get_or_create(user=u, defaults={"bio": bio}); users.append(u)
        for a in users:
            for b in users:
                if a != b: Follow.objects.get_or_create(follower=a, following=b)
        self.stdout.write("Seeded users ada, grace, linus (password demo12345).")
