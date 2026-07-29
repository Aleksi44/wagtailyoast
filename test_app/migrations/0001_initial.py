import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    # Pinned to the first wagtailcore migration rather than whichever
    # one happened to be latest when this was generated, so the test app
    # migrates on every supported Wagtail version.
    dependencies = [
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="YoastTestPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("keywords", models.CharField(blank=True, default="", max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
