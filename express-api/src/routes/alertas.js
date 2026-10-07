const express = require('express');
const router = express.Router();
const pool = require('../config/database');

// GET /alertas-externas - List all
router.get('/', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM alertas_externas WHERE estado = TRUE');
        res.json(rows);
    } catch (err) {
        next(err);
    }
});

// POST /alertas-externas - Create
router.post('/', async (req, res, next) => {
    try {
        const { mensaje, prioridad } = req.body;
        const [result] = await pool.query(
            'INSERT INTO alertas_externas (mensaje, prioridad) VALUES (?, ?)',
            [mensaje, prioridad || 'media']
        );
        res.status(201).json({ id: result.insertId, mensaje, prioridad: prioridad || 'media' });
    } catch (err) {
        next(err);
    }
});

// PUT /alertas-externas/:id - Update estado
router.put('/:id', async (req, res, next) => {
    try {
        const { mensaje, prioridad } = req.body;
        const [result] = await pool.query(
            'UPDATE alertas_externas SET mensaje = ?, prioridad = ? WHERE id = ? AND estado = TRUE',
            [mensaje, prioridad, req.params.id]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Alerta no encontrada' });
        }
        res.json({ id: req.params.id, mensaje, prioridad });
    } catch (err) {
        next(err);
    }
});

// DELETE /alertas-externas/:id - Soft delete
router.delete('/:id', async (req, res, next) => {
    try {
        const [result] = await pool.query(
            'UPDATE alertas_externas SET estado = FALSE WHERE id = ? AND estado = TRUE',
            [req.params.id]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Alerta no encontrada' });
        }
        res.json({ message: 'Alerta eliminada' });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
