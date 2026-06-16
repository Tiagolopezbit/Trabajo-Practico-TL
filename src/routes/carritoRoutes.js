const express = require('express');
const router = express.Router();
const { getCarrito, agregarAlCarrito, quitarDelCarrito } = require('../controllers/carritoController');
const verificarToken = require('../middlewares/authMiddleware');

router.get('/', verificarToken, getCarrito);
router.post('/', verificarToken, agregarAlCarrito);
router.delete('/:productoId', verificarToken, quitarDelCarrito);

module.exports = router;
