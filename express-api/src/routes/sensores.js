const express = require('express');
const router = express.Router();
const pool = require('../config/database');

router.get('/', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM sensores_externos WHERE estado = TRUE');
        res.json(rows);
    } catch (err) {
        next(err);
    }
});

router.post('/', async (req, res, next) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const [result] = await pool.query(
            'INSERT INTO sensores_externos (tipo, valor_actual, ubicacion, estado) VALUES (?, ?, ?, TRUE)',
            [tipo, valor_actual, ubicacion]
        );
        const [rows] = await pool.query('SELECT * FROM sensores_externos WHERE id = ?', [result.insertId]);
        res.status(201).json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.get('/:id', async (req, res, next) => {
    try {
        const [rows] = await pool.query(
            'SELECT * FROM sensores_externos WHERE id = ? AND estado = TRUE',
            [req.params.id]
        );
        if (rows.length === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        res.json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.put('/:id', async (req, res, next) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const [result] = await pool.query(
            'UPDATE sensores_externos SET tipo = ?, valor_actual = ?, ubicacion = ?, actualizado = CURRENT_TIMESTAMP WHERE id = ? AND estado = TRUE',
            [tipo, valor_actual, ubicacion, req.params.id]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        const [rows] = await pool.query('SELECT * FROM sensores_externos WHERE id = ?', [req.params.id]);
        res.json(rows[0]);
    } catch (err) {
        next(err);
    }
});

router.delete('/:id', async (req, res, next) => {
    try {
        const [result] = await pool.query(
            'UPDATE sensores_externos SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id = ? AND estado = TRUE',
            [req.params.id]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        res.json({ message: 'Sensor eliminado' });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
