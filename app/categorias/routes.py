from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.models import db, Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

# READ (Consulta)
@categorias_bp.route('/')
@login_required
def index():
    categorias = Categoria.query.all()
    return render_template('categorias/index.html', categorias=categorias)

# CREATE (Registro)
@categorias_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nueva = Categoria(nombre=request.form['nombre'])
        db.session.add(nueva)
        db.session.commit()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('categorias.index'))
    return render_template('categorias/form.html')

# UPDATE (Modificación)
@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        db.session.commit()
        flash('Categoría actualizada correctamente', 'success')
        return redirect(url_for('categorias.index'))
    return render_template('categorias/form.html', categoria=categoria)

# DELETE (Eliminación)
@categorias_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    cat = Categoria.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Categoría eliminada', 'success')
    return redirect(url_for('categorias.index'))