const mongoose = require('mongoose');

const itemOrdenSchema = new mongoose.Schema({
  producto: { type: mongoose.Schema.Types.ObjectId, ref: 'Producto', required: true },
  cantidad: { type: Number, required: true },
  precio: { type: Number, required: true },
  variante: {
    talla: { type: String },
    color: { type: String }
  }
});

const ordenSchema = new mongoose.Schema({
  usuario: { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario', required: true },
  items: [itemOrdenSchema],
  total: { type: Number, required: true },
  estado: { type: String, enum: ['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado'], default: 'pendiente' },
  direccionEnvio: { type: String }
}, { timestamps: true });

module.exports = mongoose.model('Orden', ordenSchema);