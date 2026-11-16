const express = require('express');
const router = express.Router();
const pool = require('../config/database');

router.get('/', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM lecturas_externas WHERE estado = TRUE ORDER BY timestamp DESC');
        res.json(rows);
    } catch (err) {
        next(err);
    }
});

router.post('/', async (req, res, next) => {
    try {
        const { sensor_id, valor, timestamp } = req.body;
        const [result] = await pool.query(
            'INSERT INTO lecturas_externas (sensor_id, valor, timestamp, estado) VALUES (?, ?, ?, TRUE)',
            [sensor_id, valor, timestamp || new Date()]
        );
        const [rows] = await pool.query('SELECT * FROM lecturas_externas WHERE id = ?', [result.insertId]);
        res.status(201).json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.get('/:id', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM lecturas_externas WHERE id = ? AND estado = TRUE', [req.params.id]);
        if (rows.length === 0) return res.status(404).json({ error: 'Lectura no encontrada' });
        res.json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.put('/:id', async (req, res, next) => {
    try {
        const { sensor_id, valor, timestamp } = req.body;
        const [result] = await pool.query(
            'UPDATE lecturas_externas SET sensor_id = ?, valor = ?, timestamp = ?, actualizado = CURRENT_TIMESTAMP WHERE id = ? AND estado = TRUE',
            [sensor_id, valor, timestamp || new Date(), req.params.id]
        );
        if (result.affectedRows === 0) return res.status(404).json({ error: 'Lectura no encontrada' });
        const [rows] = await pool.query('SELECT * FROM lecturas_externas WHERE id = ?', [req.params.id]);
        res.json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.delete('/:id', async (req, res, next) => {
    try {
        const [result] = await pool.query(
            'UPDATE lecturas_externas SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id = ? AND estado = TRUE',
            [req.params.id]
        );
        if (result.affectedRows === 0) return res.status(404).json({ error: 'Lectura no encontrada' });
        res.json({ message: 'Lectura eliminada' });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
