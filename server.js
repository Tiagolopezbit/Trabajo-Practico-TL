const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
dotenv.config();

const productoRoutes = require('./src/routes/productoRoutes');

const app = express();
app.use(express.json());

// Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('Conectado a MongoDB ✅'))
  .catch((err) => console.log('Error de conexión:', err));

// Rutas
app.use('/api/productos', productoRoutes);

app.get('/', (req, res) => {
  res.json({ message: 'API E-commerce funcionando ✅' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});
