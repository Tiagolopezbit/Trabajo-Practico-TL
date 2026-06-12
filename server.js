const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
dotenv.config();

const productoRoutes = require('./src/routes/productoRoutes');
const authRoutes = require('./src/routes/authRoutes');
const carritoRoutes = require('./src/routes/carritoRoutes');
const ordenRoutes = require('./src/routes/ordenRoutes');
const resenaRoutes = require('./src/routes/resenaRoutes');
const cuponRoutes = require('./src/routes/cuponRoutes');
const facturaRoutes = require('./src/routes/facturaRoutes');

const app = express();
app.use(express.json());
app.use(express.static('public'));

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('Conectado a MongoDB ✅'))
  .catch((err) => console.log('Error de conexión:', err));

app.use('/api/productos', productoRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/carrito', carritoRoutes);
app.use('/api/ordenes', ordenRoutes);
app.use('/api/resenas', resenaRoutes);
app.use('/api/cupones', cuponRoutes);
app.use('/api/facturas', facturaRoutes);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});