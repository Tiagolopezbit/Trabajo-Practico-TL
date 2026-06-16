const mongoose = require('mongoose');

const varianteSchema = new mongoose.Schema({
  talla: { type: String },
  color: { type: String },
  stock: { type: Number, default: 0 }
});

const productoSchema = new mongoose.Schema({
  nombre: { type: String, required: true },
  descripcion: { type: String },
  precio: { type: Number, required: true },
  categoria: { type: String },
  variantes: [varianteSchema],
  imagen: { type: String }
}, { timestamps: true });

module.exports = mongoose.model('Producto', productoSchema);
