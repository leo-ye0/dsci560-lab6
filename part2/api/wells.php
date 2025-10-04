<?php
require_once 'config.php';

try {
    $stmt = $pdo->query("SELECT * FROM wells");
    $wells = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($wells);
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to fetch wells data: ' . $e->getMessage()]);
}
?>