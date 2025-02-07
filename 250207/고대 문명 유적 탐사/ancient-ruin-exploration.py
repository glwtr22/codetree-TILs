# 13:10 ~

# 시계 방향 90도 회전 코드
def rotate(arr, si, sj):
    narr = [x[:] for x in arr]
    for i in range(3):
        for j in range(3):
            narr[si+i][sj+j] = arr[si+3-j-1][sj+i]
    return narr

def bfs(arr, v, si, sj, clr):
    # 생성
    q = []
    sset = set()
    cnt = 0

    # 초기
    q.append((si, sj))
    sset.add((si, sj))
    v[si][sj] = 1
    cnt += 1

    # 큐 돌리기
    while q:
        ci, cj = q.pop(0)
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci+di, cj+dj
            if 0<=ni<5 and 0<=nj<5 and v[ni][nj] == 0 and arr[ci][cj] == arr[ni][nj]:
                q.append((ni, nj))
                v[ni][nj] = 1
                sset.add((ni, nj))
                cnt += 1

    if cnt >= 3:    # 유물이면 : cnt 리턴 + clr==1이면 0으로 clear
        if clr == 1:
            for i, j in sset:
                arr[i][j] = 0
        return cnt
    else:
        return 0


def count_clear(arr, clr):      # clr==1인 경우 3개 이상의 값들을 0으로 클리어
    v = [[0]*5 for _ in range(5)]
    cnt = 0
    for i in range(5):
        for j in range(5):  #미방문인 경우 같은 값이면 fill
            if v[i][j] == 0:
                # 같은 값이면, 3개 이상인 경우
                t = bfs(arr, v, i, j, clr)
                cnt += t

    return cnt

K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]
lst = list(map(int, input().split()))
ans = []

for _ in range(K): # K턴 진행(유물 없는 경우, 즉시 종료)
    # [1] 탐사 (회전) 진행
    mx_cnt = 0
    for rot in range(1, 4):    # 회전 수 -> 열 -> 행 (작은 순)
        for sj in range(3):
            for si in range(3):
                # rot 횟수 만큼 90도 시계 방향 회전 => narr
                narr = [x[:] for x in arr]        # deepcopy보다 빠른 복사 (회전 : 메이즈러너 문제 참고)
                for _ in range(rot):
                    narr = rotate(narr, si, sj)

                # 유물 개수 카운트
                t = count_clear(narr, 0)
                if mx_cnt < t:           # 최대 개수일 때의 상태 marr에 보존
                    mx_cnt = t
                    marr = narr

    # 유물이 없는 경우 턴 즉시 종료
    if mx_cnt == 0:
        break

    # [2] 연쇄 획득 진행
    cnt = 0
    arr = marr
    while True:
        t = count_clear(arr, 1)
        if t == 0:
            break   # 연쇄 획득 종료 -> 다음 턴으로 이동

        cnt += t    # 획득한 유물 개수 누적

        # arr의 0 값인 부분 리스트에서 순서대로 추가
        for j in range(5):
            for i in range(4, -1, -1):
                if arr[i][j] == 0:
                    arr[i][j] = lst.pop(0)

    ans.append(cnt)  # 이번 턴 연쇄 획득한 개수 추가하기

print(*ans)


'''
유물 조각 7가지 1~7로 표현
5x5 격자 내에서 3x3 격자를 선택해 90', 180', 270' 중 하나의 각도만큼 회전
선택된 격자는 항상 회전 진행해야만 함

[회전 목표]
유물 1차 획득 가치 최대화 > 회전 각도가 가장 작은 방법 > 회전 중심 좌표의 열이 작은 > 회전 중심 좌표의 행이 작은

[유믈 획득]
같은 유물 3개 이상 연결 시, 유물이 되고 사라진다
유물 가치는 유물 조각 개수

사라진 후에는 열 번호 작은 순서, 그 다음 행 번호 작은 순서로 숫자 새로 생겨난다

유물이 채워진 후에 다시 유물 생겨날 수 있고,
유물이 생기지 않을 때까지 반복

탐사(회전) ~ 유물 연쇄 획득까지 1턴
총 K턴 진행, K턴 이전에 유물 획득 불가 시, 종료
'''