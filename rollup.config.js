import resolve from 'rollup-plugin-node-resolve';
import replace from 'rollup-plugin-replace';
import commonjs from 'rollup-plugin-commonjs';
import babel from 'rollup-plugin-babel';

import pkg from './package.json';

const NODE_ENV = JSON.stringify(process.env.NODE_ENV || 'development');

export default {
  input: pkg.entry,
  output: { file: pkg.main, name: pkg.name, format: 'iife' },
  plugins: [
    resolve({ browser: true }),
    replace({ 'process.env.NODE_ENV': NODE_ENV }),
    commonjs(),
    babel({ exclude: 'node_modules/**' }),
  ],
};
