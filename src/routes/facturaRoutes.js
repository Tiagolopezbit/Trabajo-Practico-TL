const express = require('express');
const router = express.Router();
const { generarFactura } = require('../controllers/facturaController');
const verificarToken = require('../middlewares/authMiddleware');

router.get('/:ordenId', verificarToken, generarFactura);

module.exports = router;
