const express = require('express');
const router = express.Router();
const pool = require('../config/database');

// GET /sensores-externos - List all
router.get('/', async (req, res, next) => {
    try {
        const [rows] = await pool.query('SELECT * FROM sensores_externos WHERE estado = TRUE');
        res.json(rows);
    } catch (err) {
        next(err);
    }
});

// POST /sensores-externos - Create
router.post('/', async (req, res, next) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const [result] = await pool.query(
            'INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES (?, ?, ?)',
            [tipo, valor_actual, ubicacion]
        );
        res.status(201).json({ id: result.insertId, tipo, valor_actual, ubicacion });
    } catch (err) {
        next(err);
    }
});

// GET /sensores-externos/:id - Get one
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

// PUT /sensores-externos/:id - Update
router.put('/:id', async (req, res, next) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const [result] = await pool.query(
            'UPDATE sensores_externos SET tipo = ?, valor_actual = ?, ubicacion = ? WHERE id = ? AND estado = TRUE',
            [tipo, valor_actual, ubicacion, req.params.id]
        );
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Sensor no encontrado' });
        }
        res.json({ id: req.params.id, tipo, valor_actual, ubicacion });
    } catch (err) {
        next(err);
    }
});

// DELETE /sensores-externos/:id - Soft delete
router.delete('/:id', async (req, res, next) => {
    try {
        const [result] = await pool.query(
            'UPDATE sensores_externos SET estado = FALSE WHERE id = ? AND estado = TRUE',
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
