# Generated by Django 5.1.5 on 2025-02-02 02:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configpanel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('prompt_type', models.CharField(choices=[('analysis', 'Analysis Prompt'), ('rewrite', 'Rewrite Prompt')], help_text='Выберите тип промпта (анализ или переформулирование)', max_length=20, verbose_name='Тип промпта')),
                ('content', models.TextField(help_text='Введите текст промпта', verbose_name='Текст промпта')),
                ('is_active', models.BooleanField(default=True, help_text='Флаг активности промпта', verbose_name='Активен')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Промпт',
                'verbose_name_plural': 'Промпты',
            },
        ),
        migrations.AlterModelOptions(
            name='adjectivetocountry',
            options={'verbose_name': 'Прилагательное к стране', 'verbose_name_plural': 'Прилагательные к странам'},
        ),
        migrations.AlterModelOptions(
            name='botconfig',
            options={'verbose_name': 'Конфигурация бота', 'verbose_name_plural': 'Конфигурации ботов'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='feed',
            options={'verbose_name': 'Источник', 'verbose_name_plural': 'Источники'},
        ),
        migrations.AlterModelOptions(
            name='keyword',
            options={'verbose_name': 'Ключевое слово', 'verbose_name_plural': 'Ключевые слова'},
        ),
        migrations.AlterModelOptions(
            name='newsarticle',
            options={'verbose_name': 'Новостная статья', 'verbose_name_plural': 'Новостные статьи'},
        ),
        migrations.AlterModelOptions(
            name='stopword',
            options={'verbose_name': 'Стоп-слово', 'verbose_name_plural': 'Стоп-слова'},
        ),
        migrations.AlterModelOptions(
            name='telegramadmin',
            options={'verbose_name': 'Telegram администратор', 'verbose_name_plural': 'Telegram администраторы'},
        ),
        migrations.RemoveField(
            model_name='newsarticle',
            name='date_updated',
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Дата и время последнего обновления записи', verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='adjectivetocountry',
            name='adjective',
            field=models.CharField(help_text='Введите прилагательное или сокращение, которое соответствует стране (например, "российский", "рф")', max_length=100, unique=True, verbose_name='Прилагательное/Форма'),
        ),
        migrations.AlterField(
            model_name='adjectivetocountry',
            name='country',
            field=models.ForeignKey(help_text='Выберите страну, к которой относится это прилагательное', on_delete=django.db.models.deletion.CASCADE, related_name='adjectives', to='configpanel.country', verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='botconfig',
            name='name',
            field=models.CharField(default='DefaultBotConfig', help_text='Введите название конфигурации для бота', max_length=50, verbose_name='Название конфигурации'),
        ),
        migrations.AlterField(
            model_name='botconfig',
            name='token',
            field=models.CharField(help_text='Введите токен для доступа к Telegram боту', max_length=255, verbose_name='Токен бота'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(help_text='Введите название страны (например, Россия, Китай)', max_length=100, unique=True, verbose_name='Название страны'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='feed_type',
            field=models.CharField(choices=[('rss', 'RSS-лента'), ('sitemap', 'Sitemap')], default='rss', help_text='Выберите тип источника: RSS или Sitemap', max_length=10, verbose_name='Тип источника'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='feed_url',
            field=models.URLField(help_text='Введите URL RSS-ленты или Sitemap', unique=True, verbose_name='URL источника'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='word',
            field=models.CharField(help_text='Введите ключевое слово для анализа текста (например, "сотрудничество", "договор")', max_length=100, unique=True, verbose_name='Ключевое слово'),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата и время добавления статьи в базу данных', verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='feed',
            field=models.ForeignKey(blank=True, help_text='Выберите источник, из которого была получена статья', null=True, on_delete=django.db.models.deletion.SET_NULL, to='configpanel.feed', verbose_name='Источник'),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='link',
            field=models.URLField(help_text='Введите ссылку на оригинальную статью', verbose_name='Ссылка на статью'),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='original_text',
            field=models.TextField(blank=True, help_text='Оригинальный текст статьи, полученный при парсинге', null=True, verbose_name='Оригинальный текст'),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='rewritten_text',
            field=models.TextField(blank=True, help_text='Текст статьи, переписанный ИИ', null=True, verbose_name='Переписанный текст'),
        ),
        migrations.AlterField(
            model_name='stopword',
            name='word',
            field=models.CharField(help_text='Введите стоп-слово для фильтрации нежелательных статей (например, "война", "терроризм")', max_length=100, unique=True, verbose_name='Стоп-слово'),
        ),
        migrations.AlterField(
            model_name='telegramadmin',
            name='telegram_id',
            field=models.BigIntegerField(help_text='Введите Telegram ID администратора, которому будут отправляться уведомления', unique=True, verbose_name='Telegram ID администратора'),
        ),
    ]
