const express = require('express');
const router = express.Router();
const pool = require('../config/database');

router.get('/', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM alertas_externas WHERE estado = TRUE');
        res.json(rows);
    } catch (err) {
        next(err);
    }
});

router.post('/', async (req, res, next) => {
    try {
        const { mensaje, prioridad } = req.body;
        const [result] = await pool.query(
            'INSERT INTO alertas_externas (mensaje, prioridad, estado) VALUES (?, ?, TRUE)',
            [mensaje, prioridad || 'media']
        );
        const [rows] = await pool.query('SELECT * FROM alertas_externas WHERE id = ?', [result.insertId]);
        res.status(201).json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.put('/:id', async (req, res, next) => {
    try {
        const { mensaje, prioridad } = req.body;
        const [result] = await pool.query(
            'UPDATE alertas_externas SET mensaje = ?, prioridad = ?, actualizado = CURRENT_TIMESTAMP WHERE id = ? AND estado = TRUE',
            [mensaje, prioridad, req.params.id]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Alerta no encontrada' });
        }
        const [rows] = await pool.query('SELECT * FROM alertas_externas WHERE id = ?', [req.params.id]);
        res.json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.delete('/:id', async (req, res, next) => {
    try {
        const [result] = await pool.query(
            'UPDATE alertas_externas SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id = ? AND estado = TRUE',
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
