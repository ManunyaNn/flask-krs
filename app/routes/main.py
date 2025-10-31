from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Map, Grenade, Video
from app.forms import VideoForm, EditVideoForm 
from app import db
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Главная страница"""
    maps = Map.query.all()
    grenades = Grenade.query.all()
    return render_template('index.html', maps=maps, grenades=grenades)

@bp.route('/videos')
def videos():
    """Страница с видео по выбранной карте и гранате"""
    # Получаем параметры из URL
    map_id = request.args.get('map', type=int)
    grenade_id = request.args.get('grenade', type=int)
    
    # Проверяем, что параметры переданы
    if not map_id or not grenade_id:
        # Если параметров нет, перенаправляем на главную
        return redirect(url_for('main.index'))
    
    # Ищем карту и гранату в базе
    map_obj = Map.query.get_or_404(map_id)
    grenade_obj = Grenade.query.get_or_404(grenade_id)
    
    # Ищем видео по карте и гранате
    videos_list = Video.query.filter_by(
        map_id=map_id, 
        grenade_id=grenade_id
    ).order_by(Video.created_at.desc()).all()
    
    return render_template(
        'videos.html',
        videos=videos_list,
        map=map_obj,
        grenade=grenade_obj
    )

@bp.route('/profile')
@login_required
def profile():
    """Страница профиля пользователя"""
    return render_template('profile.html', title='Профиль')

@bp.route('/test-db')
def test_db():
    """Тестовый маршрут для проверки БД"""
    maps = Map.query.all()
    grenades = Grenade.query.all()
    videos = Video.query.all()
    
    result = {
        'maps': [{'id': m.id, 'name': m.name} for m in maps],
        'grenades': [{'id': g.id, 'name': g.name} for g in grenades],
        'videos_count': len(videos)
    }
    
    return jsonify(result)

@bp.route('/health')
def health_check():
    """API проверки здоровья"""
    return jsonify({'status': 'ok'})

@bp.route('/add-video', methods=['GET', 'POST'])
@login_required
def add_video():
    """Добавление нового видео"""
    form = VideoForm()
    
    if form.validate_on_submit():
        # Создаем новое видео
        video = Video(
            title=form.title.data,
            description=form.description.data,
            video_url=form.video_url.data,
            author_id=current_user.id,
            map_id=form.map_id.data,
            grenade_id=form.grenade_id.data,
            created_at=datetime.utcnow()
        )
        
        # Сохраняем в базу
        db.session.add(video)
        db.session.commit()
        
        flash('✅ Видео успешно добавлено!', 'success')
        return redirect(url_for('main.videos', map=form.map_id.data, grenade=form.grenade_id.data))
    
    return render_template('add_video.html', title='Добавить видео', form=form)

@bp.route('/edit-video/<int:video_id>', methods=['GET', 'POST'])
@login_required
def edit_video(video_id):
    """Редактирование видео"""
    # Находим видео в базе
    video = Video.query.get_or_404(video_id)
    
    # Проверяем права доступа - только автор или администратор может редактировать
    if video.author_id != current_user.id and current_user.role != 'admin':
        flash('❌ У вас нет прав для редактирования этого видео', 'danger')
        return redirect(url_for('main.videos', map=video.map_id, grenade=video.grenade_id))
    
    form = EditVideoForm()
    
    # Заполняем форму текущими данными видео
    if request.method == 'GET':
        form.title.data = video.title
        form.description.data = video.description
        form.video_url.data = video.video_url
        form.map_id.data = video.map_id
        form.grenade_id.data = video.grenade_id
    
    if form.validate_on_submit():
        # Обновляем данные видео
        video.title = form.title.data
        video.description = form.description.data
        
        # Если изменилась ссылка - обновляем превью
        if video.video_url != form.video_url.data:
            video.video_url = form.video_url.data
            from app.utils import get_youtube_thumbnail
            video.thumbnail_url = get_youtube_thumbnail(video.video_url, quality='hqdefault')
        
        video.map_id = form.map_id.data
        video.grenade_id = form.grenade_id.data
        video.updated_at = datetime.utcnow()
        
        # Сохраняем изменения
        db.session.commit()
        
        flash('✅ Видео успешно обновлено!', 'success')
        return redirect(url_for('main.videos', map=video.map_id, grenade=video.grenade_id))
    
    return render_template('edit_video.html', title='Редактировать видео', form=form, video=video)

@bp.route('/delete-video/<int:video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    """Удаление видео"""
    # Находим видео в базе
    video = Video.query.get_or_404(video_id)
    
    # Сохраняем ID для редиректа
    map_id = video.map_id
    grenade_id = video.grenade_id
    
    # Проверяем права доступа - только автор или администратор может удалять
    if video.author_id != current_user.id and current_user.role != 'admin':
        flash('❌ У вас нет прав для удаления этого видео', 'danger')
        return redirect(url_for('main.videos', map=map_id, grenade=grenade_id))
    
    # Удаляем видео
    db.session.delete(video)
    db.session.commit()
    
    flash('✅ Видео успешно удалено!', 'success')
    return redirect(url_for('main.videos', map=map_id, grenade=grenade_id))

@bp.route('/export-links')
def export_links():
    """Экспорт ссылок на видео в текстовый файл"""
    # Получаем параметры из URL
    map_id = request.args.get('map', type=int)
    grenade_id = request.args.get('grenade', type=int)
    
    if not map_id or not grenade_id:
        flash('Пожалуйста, выберите карту и гранату', 'warning')
        return redirect(url_for('main.index'))
    
    # Ищем карту и гранату
    map_obj = Map.query.get_or_404(map_id)
    grenade_obj = Grenade.query.get_or_404(grenade_id)
    
    # Ищем видео
    videos = Video.query.filter_by(
        map_id=map_id, 
        grenade_id=grenade_id
    ).order_by(Video.created_at.desc()).all()
    
    # Создаем содержимое файла
    file_content = f"""GrenadeGuide - Экспорт ссылок на видео
Карта: {map_obj.display_name}
Граната: {grenade_obj.display_name}
Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Количество видео: {len(videos)}

Ссылки на видео:
{"="*50}

"""
    
    for i, video in enumerate(videos, 1):
        file_content += f"{i}. {video.title}\n"
        file_content += f"   Ссылка: {video.video_url}\n"
        if video.description:
            file_content += f"   Описание: {video.description}\n"
        file_content += f"   Автор: {video.author.username}\n"
        file_content += f"   Добавлено: {video.created_at.strftime('%d.%m.%Y')}\n"
        file_content += "-" * 30 + "\n"
    
    file_content += f"\nВсего видео: {len(videos)}"
    
    # Создаем response с файлом (ИСПРАВЛЕННАЯ ЧАСТЬ)
    from io import BytesIO
    from flask import send_file
    
    # Создаем файл в памяти в БИНАРНОМ режиме
    file_buffer = BytesIO()
    file_buffer.write(file_content.encode('utf-8'))  # ← Кодируем в bytes
    file_buffer.seek(0)
    
    # Генерируем имя файла
    filename = f"grenadeguide_{map_obj.name}_{grenade_obj.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    
    return send_file(
        file_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain; charset=utf-8'
    )