const Usuario = require('../models/Usuario');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// Registro
const registro = async (req, res) => {
  try {
    const { nombre, email, password } = req.body;
    const usuarioExiste = await Usuario.findOne({ email });
    if (usuarioExiste) return res.status(400).json({ message: 'El email ya está registrado' });

    const usuario = new Usuario({ nombre, email, password });
    await usuario.save();
    res.status(201).json({ message: 'Usuario registrado ✅' });
  } catch (error) {
    res.status(500).json({ message: 'Error al registrar usuario' });
  }
};

// Login
const login = async (req, res) => {
  try {
    const { email, password } = req.body;
    const usuario = await Usuario.findOne({ email });
    if (!usuario) return res.status(400).json({ message: 'Email o contraseña incorrectos' });

    const passwordValido = await bcrypt.compare(password, usuario.password);
    if (!passwordValido) return res.status(400).json({ message: 'Email o contraseña incorrectos' });

    const token = jwt.sign(
      { id: usuario._id, rol: usuario.rol },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({ token, usuario: { id: usuario._id, nombre: usuario.nombre, email: usuario.email, rol: usuario.rol } });
  } catch (error) {
    res.status(500).json({ message: 'Error al iniciar sesión' });
  }
};

module.exports = { registro, login };
