const Producto = require('../models/Producto');

// Obtener todos los productos
const getProductos = async (req, res) => {
  try {
    const productos = await Producto.find();
    res.json(productos);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener productos' });
  }
};

// Crear un producto
const crearProducto = async (req, res) => {
  try {
    const producto = new Producto(req.body);
    await producto.save();
    res.status(201).json(producto);
  } catch (error) {
    res.status(500).json({ message: 'Error al crear producto' });
  }
};

// Obtener un producto por ID
const getProductoById = async (req, res) => {
  try {
    const producto = await Producto.findById(req.params.id);
    if (!producto) return res.status(404).json({ message: 'Producto no encontrado' });
    res.json(producto);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener producto' });
  }
};

// Actualizar un producto
const actualizarProducto = async (req, res) => {
  try {
    const producto = await Producto.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!producto) return res.status(404).json({ message: 'Producto no encontrado' });
    res.json(producto);
  } catch (error) {
    res.status(500).json({ message: 'Error al actualizar producto' });
  }
};

// Eliminar un producto
const eliminarProducto = async (req, res) => {
  try {
    const producto = await Producto.findByIdAndDelete(req.params.id);
    if (!producto) return res.status(404).json({ message: 'Producto no encontrado' });
    res.json({ message: 'Producto eliminado ✅' });
  } catch (error) {
    res.status(500).json({ message: 'Error al eliminar producto' });
  }
};

module.exports = { getProductos, crearProducto, getProductoById, actualizarProducto, eliminarProducto };
