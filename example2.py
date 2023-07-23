from tqdm import tqdm
import time

total_iterations = 100
current_iteration = 0

while True:
    # Выполнение какой-то работы
    time.sleep(1)  # имитация работы
    
    # Обновление состояния прогресса
    current_iteration += 1
    bar = tqdm(total=total_iterations)
    bar.update(current_iteration)
    
    # Проверка условия завершения
    if current_iteration == total_iterations:
        break

# Дополнительные действия после завершения цикла
print("Цикл завершен")
