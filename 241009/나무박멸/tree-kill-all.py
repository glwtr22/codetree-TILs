n, m, k, c = map(int, input().split())

mat = []
for _ in range(n):
    mat.append(list(map(int, input().split())))

Q = [[0 for _ in range(n)] for _ in range(n)]
count = [[0 for _ in range(n)] for _ in range(n)]
dead = [[0 for _ in range(n)] for _ in range(n)]

# 총 박멸한 그루 수
total = 0

# 나무의 성장
def grow(mat):
    for i in range(n):
        for j in range(n):
            if mat[i][j] and mat[i][j] != -1:
                mat[i][j] += 1

# 나무의 확산
def spread(mat):
    # 몫 Q에 저장
    for i in range(n):
        for j in range(n):
            cnt = 0
            if mat[i][j] and mat[i][j] != -1 and not dead[i][j]:
                for di, dj in ([-1, 0], [0, -1], [1, 0], [0, 1]):
                    dx = i + di
                    dy = j + dj
                    if 0 <= dx < n and 0 <= dy < n and mat[dx][dy] == 0:
                        cnt += 1

                Q[i][j] =  mat[i][j] // cnt
    
    # Q에 저장된 값 합산 후 mat에 저장
    for i in range(n):
        for j in range(n):
            t = 0
            if not mat[i][j] and not dead[i][j]:
                for di, dj in ([-1, 0], [0, -1], [1, 0], [0, 1]):
                    dx = i + di
                    dy = j + dj
                    if 0 <= dx < n and 0 <= dy < n:
                        t += Q[dx][dy]
            mat[i][j] = t

# 각 위치 별 최대 박멸 그루 수 저장
def check(mat):
    for i in range(n):
        for j in range(n):
            K = 0
            if mat[i][j] and mat[i][j] != -1:   # 나무인 경우에
                # 네 방향 대각선의 k 범위에 대해서
                for di, dj in ([-1, 0], [0, -1], [1, 0], [0, 1]):
                    for dk in range(1, k+1):
                        dx = i + di * dk
                        dy = j + dj * dk
                        if 0 <= dx < n and 0 <= dy < n and not mat[dx][dy] and mat[dx][dy] != -1:
                            K += mat[dx][dy]
            count[i][j] = k
    
    MAX = 0
    for i in range(n):
        for j in range(m):
            if count[i][j] > MAX:
                ai, aj = i, j
            MAX = count[i][j]                       

    # 최대 그루 수 박멸하는 위치 반환    
    return (ai, aj)

# 반환 받은 위치에서 제초제 뿌리기
def kill(mat, I, J):
    global total
    dead[I][J] = c
    for di, dj in ([-1, 0], [0, -1], [1, 0], [0, 1]):
        for dk in range(1, k+1):
            dx = I + di * dk
            dy = J + dj * dk
            if 0 <= dx < n and 0 <= dy < n:
                total += mat[dx][dy]
                dead[dx][dy] = c
                

# 일 년 후에, 제초제 -1씩
def one(dead):
    for i in range(n):
        for j in range(n):
            if dead[i][j]:
                dead[i][j] -= 1


# m년 간 반복
for _ in range(m):
    grow(mat)
    spread(mat)
    I, J = check(mat)
    kill(mat, I, J)
    one(dead)

print(total)




'''
3:00 ~

m년 동안 박멸한 총 나무의 그루 수 ??

격자 크기 n, 박멸 진행 년 수 m, 제초제의 확산 범위 k, 제초제가 남아있는 년 수 c

1. 성장은 모든 나무에게 동시에 일어남 (1씩 성장)
2. 총 번식 가능한 칸의 개수만큼 나누어진 그루 수만큼 번식 (나머지 버림) : 번식은 퍼지는거, 성장 > 번식
3. 나무 가장 많이 박멸되는 칸에 제초제 뿌리기 -> 대각선 방향으로 k만큼 전파, c년만큼 제초제 남아
4. 같은 경우 : 행 작은 순 > 열 작은 순
'''