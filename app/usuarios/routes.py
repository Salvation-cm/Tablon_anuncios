from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.models import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# READ (Consulta)
@usuarios_bp.route('/')
@login_required
def index():
    usuarios = Usuario.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios)

# CREATE (Registro)
@usuarios_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nuevo = Usuario(
            nombre=request.form['nombre'],
            email=request.form['email'],
            password=request.form['password']
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuarios.index'))
    return render_template('usuarios/form.html')

# UPDATE (Modificación) <--- ESTO ERA LO QUE FALTABA
@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']
        # Solo actualizamos la contraseña si el usuario escribió una nueva
        if request.form['password']:
            usuario.password = request.form['password']
        
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios.index'))
    
    return render_template('usuarios/form.html', usuario=usuario)

# DELETE (Eliminación)
@usuarios_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado', 'success')
    return redirect(url_for('usuarios.index'))