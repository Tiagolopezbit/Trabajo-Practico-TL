const Resena = require('../models/Resena');

// Crear reseña
const crearResena = async (req, res) => {
  try {
    const { productoId, rating, comentario } = req.body;
    const resena = new Resena({
      producto: productoId,
      usuario: req.usuario.id,
      rating,
      comentario
    });
    await resena.save();
    res.status(201).json(resena);
  } catch (error) {
    res.status(500).json({ message: 'Error al crear reseña' });
  }
};

// Obtener reseñas de un producto
const getResenas = async (req, res) => {
  try {
    const resenas = await Resena.find({ producto: req.params.productoId }).populate('usuario', 'nombre');
    const rating = resenas.reduce((acc, r) => acc + r.rating, 0) / resenas.length;
    res.json({ resenas, ratingPromedio: rating || 0 });
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener reseñas' });
  }
};

module.exports = { crearResena, getResenas };
