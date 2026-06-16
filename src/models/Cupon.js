const mongoose = require('mongoose');

const cuponSchema = new mongoose.Schema({
  codigo: { type: String, required: true, unique: true },
  descuento: { type: Number, required: true },
  tipo: { type: String, enum: ['porcentaje', 'fijo'], default: 'porcentaje' },
  activo: { type: Boolean, default: true },
  fechaExpiracion: { type: Date }
}, { timestamps: true });

module.exports = mongoose.model('Cupon', cuponSchema);
