const Orden = require('../models/Orden');
const Carrito = require('../models/Carrito');
const Producto = require('../models/Producto');

// Crear orden desde el carrito
const crearOrden = async (req, res) => {
  try {
    const { direccionEnvio } = req.body;
    const carrito = await Carrito.findOne({ usuario: req.usuario.id }).populate('items.producto');
    if (!carrito || carrito.items.length === 0) return res.status(400).json({ message: 'El carrito está vacío' });

    // Descontar stock
    for (const item of carrito.items) {
      const producto = await Producto.findById(item.producto._id);
      if (producto.variantes.length > 0) {
        const variante = producto.variantes.find(v => v.talla === item.variante.talla && v.color === item.variante.color);
        if (variante) variante.stock -= item.cantidad;
      }
      await producto.save();
    }

    const orden = new Orden({
      usuario: req.usuario.id,
      items: carrito.items.map(item => ({
        producto: item.producto._id,
        cantidad: item.cantidad,
        precio: item.producto.precio,
        variante: item.variante
      })),
      total: carrito.total,
      direccionEnvio
    });

    await orden.save();

    // Vaciar carrito
    carrito.items = [];
    carrito.total = 0;
    await carrito.save();

    res.status(201).json(orden);
  } catch (error) {
    res.status(500).json({ message: 'Error al crear orden' });
  }
};

// Obtener órdenes del usuario
const getOrdenes = async (req, res) => {
  try {
    const ordenes = await Orden.find({ usuario: req.usuario.id }).populate('items.producto');
    res.json(ordenes);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener órdenes' });
  }
};

module.exports = { crearOrden, getOrdenes };
