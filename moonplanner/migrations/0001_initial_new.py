# Generated by Django 2.2.9 on 2020-03-03 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('moonplanner', '0001_initial'), ('moonplanner', '0002_auto_20190930_1047'), ('moonplanner', '0003_auto_20190930_1415'), ('moonplanner', '0004_auto_20190930_1800'), ('moonplanner', '0005_auto_20190930_2040'), ('moonplanner', '0006_auto_20190930_2216'), ('moonplanner', '0007_auto_20191018_1929'), ('moonplanner', '0008_auto_20191019_1733'), ('moonplanner', '0009_auto_20191019_1735')]

    initial = True

    dependencies = [
        ('evesde', '0014_delete_evename'),
        ('eveonline', '0010_alliance_ticker'),
        ('evesde', '0010_auto_20190927_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('decay_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='MarketPrice',
            fields=[
                ('type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='evesde.EveType')),
                ('average_price', models.FloatField(default=None, null=True)),
                ('adjusted_price', models.FloatField(default=None, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MiningCorporation',
            fields=[
                ('corporation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='eveonline.EveCorporationInfo')),
                ('character', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eveonline.EveCharacter')),
            ],
        ),
        migrations.CreateModel(
            name='Moon',
            fields=[
                ('moon', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='evesde.EveItem')),
                ('income', models.BigIntegerField(default=None, null=True)),
                ('system', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evesde.EveSolarSystem')),
            ],
            options={
                'permissions': (('access_moonplanner', 'Can access the moonplanner app'), ('research_moons', 'Can research all moons in the database'), ('upload_moon_scan', 'Can upload moon scans')),
            },
        ),
        migrations.CreateModel(
            name='Refinery',
            fields=[
                ('structure_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('corporation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moonplanner.MiningCorporation')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moonplanner.Moon')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evesde.EveType')),
            ],
        ),
        migrations.CreateModel(
            name='MoonProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('moon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moonplanner.Moon')),
                ('ore_type', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evesde.EveType')),
            ],
        ),
        migrations.CreateModel(
            name='ExtrationProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moonplanner.Extraction')),
                ('ore_type', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evesde.EveType')),
            ],
        ),
        migrations.AddField(
            model_name='extraction',
            name='refinery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moonplanner.Refinery'),
        ),
        migrations.AddIndex(
            model_name='moonproduct',
            index=models.Index(fields=['moon'], name='moonplanner_moon_id_5b5124_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='moonproduct',
            unique_together={('moon', 'ore_type')},
        ),
        migrations.AlterUniqueTogether(
            name='extrationproduct',
            unique_together={('extraction', 'ore_type')},
        ),
        migrations.AlterUniqueTogether(
            name='extraction',
            unique_together={('arrival_time', 'refinery')},
        ),
        migrations.RenameField(
            model_name='refinery',
            old_name='location',
            new_name='moon',
        ),
        migrations.RenameField(
            model_name='moon',
            old_name='system',
            new_name='solar_system',
        ),
        migrations.AlterField(
            model_name='refinery',
            name='moon',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='moonplanner.Moon'),
        ),
        migrations.RenameField(
            model_name='extrationproduct',
            old_name='amount',
            new_name='volume',
        ),
        migrations.RenameModel(
            old_name='ExtrationProduct',
            new_name='ExtractionProduct',
        ),
        migrations.RenameField(
            model_name='extraction',
            old_name='decay_time',
            new_name='auto_time',
        ),
        migrations.RenameField(
            model_name='extraction',
            old_name='arrival_time',
            new_name='ready_time',
        ),
        migrations.AlterField(
            model_name='extractionproduct',
            name='ore_type',
            field=models.ForeignKey(default=None, limit_choices_to=models.Q(group__category_id=25), null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evesde.EveType'),
        ),
        migrations.AlterField(
            model_name='moon',
            name='moon',
            field=models.OneToOneField(limit_choices_to={'type_id': 14}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='evesde.EveItem'),
        ),
        migrations.AlterField(
            model_name='moonproduct',
            name='ore_type',
            field=models.ForeignKey(default=None, limit_choices_to=models.Q(group__category_id=25), null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='evesde.EveType'),
        ),
        migrations.AlterField(
            model_name='refinery',
            name='type',
            field=models.ForeignKey(limit_choices_to={'group_id': 1406}, on_delete=django.db.models.deletion.CASCADE, to='evesde.EveType'),
        ),
        migrations.AlterUniqueTogether(
            name='extraction',
            unique_together={('ready_time', 'refinery')},
        ),
        migrations.AlterModelOptions(
            name='moon',
            options={},
        ),
        migrations.CreateModel(
            name='MoonPlanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('access_moonplanner', 'Can access the moonplanner app'), ('access_our_moons', 'Can access our moons and see extractions'), ('access_all_moons', 'Can access all moons in the database'), ('upload_moon_scan', 'Can upload moon scans'), ('add_mining_corporation', 'Can add mining corporation')),
                'default_permissions': (),
                'managed': False,
            },
        ),
    ]
