from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Anuncio, Categoria

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/')
@login_required
def index():
    anuncios = Anuncio.query.all()
    return render_template('anuncios/index.html', anuncios=anuncios)

@anuncios_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        nuevo = Anuncio(
            titulo=request.form['titulo'],
            contenido=request.form['contenido'],
            categoria_id=request.form['categoria_id'],
            usuario_id=current_user.id
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Anuncio creado', 'success')
        return redirect(url_for('anuncios.index'))
    return render_template('anuncios/form.html', categorias=categorias)

@anuncios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    anuncio = Anuncio.query.get_or_404(id)
    categorias = Categoria.query.all()
    if request.method == 'POST':
        anuncio.titulo = request.form['titulo']
        anuncio.contenido = request.form['contenido']
        anuncio.categoria_id = request.form['categoria_id']
        db.session.commit()
        flash('Anuncio actualizado', 'success')
        return redirect(url_for('anuncios.index'))
    return render_template('anuncios/form.html', anuncio=anuncio, categorias=categorias)

@anuncios_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    flash('Anuncio eliminado', 'success')
    return redirect(url_for('anuncios.index'))