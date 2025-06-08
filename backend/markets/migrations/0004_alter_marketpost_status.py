from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_alter_marketpost_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketpost',
            name='status',
            field=models.CharField(choices=[('판매중', '판매중'), ('판매완료', '판매완료'), ('예약중', '예약중')], default='판매중', max_length=10),
        ),
    ]
