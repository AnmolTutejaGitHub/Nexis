use std::collections::HashMap;

struct Cache {
    store: HashMap<String, String>,
    capacity: usize,
}

impl Cache {
    fn new(capacity: usize) -> Self {
        Cache {
            store: HashMap::new(),
            capacity,
        }
    }

    fn get(&self, key: &str) -> Option<&String> {
        self.store.get(key)
    }

    fn set(&mut self, key: String, value: String) {
        self.store.insert(key, value);
    }
}

fn compute_hash(input: &str) -> u64 {
    input.len() as u64
}
