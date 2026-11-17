const fs = require('node:fs');
const path = require('node:path');
const mysql = require('mysql2/promise');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });
const { construirConfig } = require('../src/config/opciones');

async function main() {
    const config = { ...construirConfig(process.env), multipleStatements: true };
    const conexion = await mysql.createConnection(config);
    try {
        console.log(`Conectado a ${config.host}:${config.port}/${config.database}`);

        const [tablas] = await conexion.query(
            "SELECT COUNT(*) AS n FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'sensores_externos'"
        );
        if (tablas[0].n > 0) {
            const [filas] = await conexion.query('SELECT COUNT(*) AS n FROM sensores_externos');
            if (filas[0].n > 0) {
                console.log(`La base ya tiene ${filas[0].n} sensores externos: no se vuelve a cargar.`);
                return;
            }
        }

        const sql = fs.readFileSync(path.join(__dirname, '..', 'schema.sql'), 'utf8');
        await conexion.query(sql);

        for (const tabla of ['sensores_externos', 'lecturas_externas', 'alertas_externas']) {
            const [filas] = await conexion.query(`SELECT COUNT(*) AS n FROM ${tabla}`);
            console.log(`  ${tabla}: ${filas[0].n} filas`);
        }
        console.log('Esquema cargado.');
    } finally {
        await conexion.end();
    }
}

main().catch((err) => {
    console.error('No se pudo cargar el esquema:', err.message);
    process.exit(1);
});
