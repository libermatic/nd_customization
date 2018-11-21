export function omit(keys, object) {
  function reducer_fn(acc, key) {
    if (!keys.includes(key)) {
      return Object.assign(acc, { [key]: object[key] });
    }
    return acc;
  }
  return Object.keys(object).reduce(reducer_fn, {});
}

export default { omit };
