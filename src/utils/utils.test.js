import test from 'ava';

import { omit } from '.';

test('omit', t => {
  const expected = { a: 1, b: 2 };
  const actual = omit(['c', 'd'], { a: 1, b: 2, c: 3, d: 4 });
  t.deepEqual(expected, actual);
});
