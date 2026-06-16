const Carrito = require('../models/Carrito');
const Producto = require('../models/Producto');

// Obtener carrito del usuario
const getCarrito = async (req, res) => {
  try {
    const carrito = await Carrito.findOne({ usuario: req.usuario.id }).populate('items.producto');
    if (!carrito) return res.json({ items: [], total: 0 });
    res.json(carrito);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener carrito' });
  }
};

// Agregar producto al carrito
const agregarAlCarrito = async (req, res) => {
  try {
    const { productoId, cantidad, variante } = req.body;
    const producto = await Producto.findById(productoId);
    if (!producto) return res.status(404).json({ message: 'Producto no encontrado' });

    let carrito = await Carrito.findOne({ usuario: req.usuario.id });
    if (!carrito) {
      carrito = new Carrito({ usuario: req.usuario.id, items: [], total: 0 });
    }

    const itemExiste = carrito.items.findIndex(item => item.producto.toString() === productoId);
    if (itemExiste >= 0) {
      carrito.items[itemExiste].cantidad += cantidad;
    } else {
      carrito.items.push({ producto: productoId, cantidad, variante });
    }

    carrito.total = carrito.items.reduce((acc, item) => acc + (producto.precio * item.cantidad), 0);
    await carrito.save();
    res.json(carrito);
  } catch (error) {
    res.status(500).json({ message: 'Error al agregar al carrito' });
  }
};

// Quitar producto del carrito
const quitarDelCarrito = async (req, res) => {
  try {
    const carrito = await Carrito.findOne({ usuario: req.usuario.id });
    if (!carrito) return res.status(404).json({ message: 'Carrito no encontrado' });

    carrito.items = carrito.items.filter(item => item.producto.toString() !== req.params.productoId);
    await carrito.save();
    res.json(carrito);
  } catch (error) {
    res.status(500).json({ message: 'Error al quitar del carrito' });
  }
};

module.exports = { getCarrito, agregarAlCarrito, quitarDelCarrito };
