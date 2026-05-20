<?php
namespace App\Services;

use App\Models\User;
use App\Exceptions\NotFoundException;

interface Repository {
    public function find(int $id): mixed;
    public function save(array $data): bool;
}

class UserService implements Repository {
    private $db;
    private array $cache = [];

    public function __construct($db) {
        $this->db = $db;
    }

    public function find(int $id): mixed {
        return $this->cache[$id] ?? null;
    }

    public function save(array $data): bool {
        $this->cache[$data['id']] = $data;
        return true;
    }

    public function createUser(array $data): User {
        return new User($data);
    }

    private function validate(array $data): bool {
        return isset($data['email']);
    }
}

function sanitize_input(string $input): string {
    return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
}

function generate_token(int $length = 32): string {
    return bin2hex(random_bytes($length));
}
