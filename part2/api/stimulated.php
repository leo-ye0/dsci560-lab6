<?php
require_once 'config.php';

try {
    $stmt = $pdo->query("SELECT * FROM stimulated_data");
    $stimulated = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($stimulated);
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to fetch stimulated data: ' . $e->getMessage()]);
}
?>