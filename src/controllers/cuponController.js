const Cupon = require('../models/Cupon');

// Crear cupón
const crearCupon = async (req, res) => {
  try {
    const cupon = new Cupon(req.body);
    await cupon.save();
    res.status(201).json(cupon);
  } catch (error) {
    res.status(500).json({ message: 'Error al crear cupón' });
  }
};

// Validar cupón
const validarCupon = async (req, res) => {
  try {
    const cupon = await Cupon.findOne({ codigo: req.params.codigo, activo: true });
    if (!cupon) return res.status(404).json({ message: 'Cupón no válido o expirado' });

    if (cupon.fechaExpiracion && cupon.fechaExpiracion < new Date()) {
      return res.status(400).json({ message: 'Cupón expirado' });
    }

    res.json({ descuento: cupon.descuento, tipo: cupon.tipo });
  } catch (error) {
    res.status(500).json({ message: 'Error al validar cupón' });
  }
};

module.exports = { crearCupon, validarCupon };
