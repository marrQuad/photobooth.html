<?php
header('Content-Type: application/json');

// Проверяем, что запрос был отправлен методом POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'error' => 'Invalid request method.']);
    exit;
}

// Получаем данные из тела запроса
$data = json_decode(file_get_contents('php://input'), true);

// Проверяем, что данные существуют
if (!isset($data['image']) || !isset($data['filename'])) {
    echo json_encode(['success' => false, 'error' => 'Missing image or filename data.']);
    exit;
}

$base64_image = $data['image'];
$filename = $data['filename'];

// Убираем заголовок "data:image/png;base64," из строки
$image_data = str_replace('data:image/png;base64,', '', $base64_image);
$image_data = str_replace(' ', '+', $image_data);
$image_data = base64_decode($image_data);

// Создаем папку 'saves', если она не существует
$save_folder = 'saves';
if (!is_dir($save_folder)) {
    mkdir($save_folder, 0777, true);
}

// Путь к файлу для сохранения
$file_path = $save_folder . '/' . basename($filename);

// Сохраняем изображение
if (file_put_contents($file_path, $image_data)) {
    echo json_encode(['success' => true, 'message' => 'Photo saved successfully.']);
} else {
    echo json_encode(['success' => false, 'error' => 'Failed to save photo.']);
}
?>