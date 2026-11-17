const test = require('node:test');
const assert = require('node:assert/strict');
const { construirConfig } = require('../src/config/opciones');

test('una URL de Aiven con ssl-mode=REQUIRED activa TLS y quita el parametro', () => {
    const cfg = construirConfig({
        MYSQL_URL: 'mysql://avnadmin:cl%40ve@mysql-x.aivencloud.com:12345/defaultdb?ssl-mode=REQUIRED'
    });
    assert.equal(cfg.host, 'mysql-x.aivencloud.com');
    assert.equal(cfg.port, 12345);
    assert.equal(cfg.user, 'avnadmin');
    assert.equal(cfg.password, 'cl@ve');
    assert.equal(cfg.database, 'defaultdb');
    assert.deepEqual(cfg.ssl, { rejectUnauthorized: false });
    assert.equal(cfg['ssl-mode'], undefined);
});

test('una URL local sin SSL no activa TLS', () => {
    const cfg = construirConfig({ MYSQL_URL: 'mysql://root:root@localhost:3306/growapp' });
    assert.equal(cfg.host, 'localhost');
    assert.equal(cfg.port, 3306);
    assert.equal(cfg.ssl, undefined);
});

test('MYSQL_SSL=true fuerza TLS aunque la URL no lo diga', () => {
    const cfg = construirConfig({ MYSQL_URL: 'mysql://u:p@h:3306/db', MYSQL_SSL: 'true' });
    assert.deepEqual(cfg.ssl, { rejectUnauthorized: false });
});

test('sin MYSQL_URL falla con un mensaje claro', () => {
    assert.throws(() => construirConfig({}), /Falta MYSQL_URL/);
});
