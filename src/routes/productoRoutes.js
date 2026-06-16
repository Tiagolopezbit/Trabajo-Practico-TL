const express = require('express');
const router = express.Router();
const { getProductos, crearProducto, getProductoById, actualizarProducto, eliminarProducto } = require('../controllers/productoController');

router.get('/', getProductos);
router.post('/', crearProducto);
router.get('/:id', getProductoById);
router.put('/:id', actualizarProducto);
router.delete('/:id', eliminarProducto);

module.exports = router;
