const express = require('express');
const router = express.Router();
const { crearCupon, validarCupon } = require('../controllers/cuponController');
const verificarToken = require('../middlewares/authMiddleware');

router.post('/', verificarToken, crearCupon);
router.get('/:codigo', validarCupon);

module.exports = router;
