const PDFDocument = require('pdfkit');
const Orden = require('../models/Orden');

const generarFactura = async (req, res) => {
  try {
    const orden = await Orden.findById(req.params.ordenId).populate('items.producto').populate('usuario', 'nombre email');
    if (!orden) return res.status(404).json({ message: 'Orden no encontrada' });

    const doc = new PDFDocument();
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename=factura-${orden._id}.pdf`);
    doc.pipe(res);

    // Encabezado
    doc.fontSize(20).text('FACTURA', { align: 'center' });
    doc.moveDown();
    doc.fontSize(12).text(`Orden ID: ${orden._id}`);
    doc.text(`Cliente: ${orden.usuario.nombre}`);
    doc.text(`Email: ${orden.usuario.email}`);
    doc.text(`Fecha: ${orden.createdAt.toLocaleDateString()}`);
    doc.text(`Dirección: ${orden.direccionEnvio}`);
    doc.moveDown();

    // Productos
    doc.fontSize(14).text('Productos:', { underline: true });
    doc.moveDown();
    orden.items.forEach(item => {
      doc.fontSize(12).text(`- ${item.producto.nombre} x${item.cantidad} - $${item.precio}`);
    });

    doc.moveDown();
    doc.fontSize(14).text(`Total: $${orden.total}`, { align: 'right' });

    doc.end();
  } catch (error) {
    res.status(500).json({ message: 'Error al generar factura' });
  }
};

module.exports = { generarFactura };
