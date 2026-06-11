const mongoose = require('mongoose');

const resenaSchema = new mongoose.Schema({
  producto: { type: mongoose.Schema.Types.ObjectId, ref: 'Producto', required: true },
  usuario: { type: mongoose.Schema.Types.ObjectId, ref: 'Usuario', required: true },
  rating: { type: Number, required: true, min: 1, max: 5 },
  comentario: { type: String }
}, { timestamps: true });

module.exports = mongoose.model('Resena', resenaSchema);
