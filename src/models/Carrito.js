const mongoose = require('mongoose');

const itemCarritoSchema = new mongoose.Schema({
  producto: { type: mongoose.Schema.Types.ObjectId, ref: 'Producto', required: true },
  cantidad: { type: Number, required: true, default: 1 },
  variante: {
    talla: { type: String },
    color: { type: String }
  }
});

const carritoSchema = new mongoose.Schema({
  usuario: { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario', required: true },
  items: [itemCarritoSchema],
  total: { type: Number, default: 0 }
}, { timestamps: true });

module.exports = mongoose.model('Carrito', carritoSchema);
