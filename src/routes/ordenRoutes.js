const express = require('express');
const router = express.Router();
const { crearOrden, getOrdenes } = require('../controllers/ordenController');
const verificarToken = require('../middlewares/authMiddleware');

router.post('/', verificarToken, crearOrden);
router.get('/', verificarToken, getOrdenes);

module.exports = router;
