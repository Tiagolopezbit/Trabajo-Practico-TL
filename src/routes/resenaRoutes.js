const express = require('express');
const router = express.Router();
const { crearResena, getResenas } = require('../controllers/resenaController');
const verificarToken = require('../middlewares/authMiddleware');

router.post('/', verificarToken, crearResena);
router.get('/:productoId', getResenas);

module.exports = router;
