import json


def load_data(filepath):
    """JSON 파일을 읽어 딕셔너리로 반환"""
    pass  # TODO


def pad_matrix(matrix, pad_size):
    """2D 행렬의 상하좌우에 pad_size만큼 0을 추가"""
    pass  # TODO


def conv2d(image, kernel):
    """패딩 없이 stride=1로 2D 컨볼루션 수행"""
    pass  # TODO


def relu(matrix):
    """음수 값을 0으로 변환한 새 행렬 반환"""
    pass  # TODO


def flatten(matrix):
    """2D 행렬을 행 우선 순서로 1D 리스트로 변환"""
    pass  # TODO


def compute_stats(matrix):
    """min, max, mean 계산하여 딕셔너리로 반환"""
    pass  # TODO


def extract_features(image, kernels):
    """각 커널로 conv2d + relu 적용한 특징맵 딕셔너리 반환"""
    pass  # TODO


def find_strongest_feature(image, kernels):
    """relu 후 합이 가장 큰 커널 이름 반환"""
    pass  # TODO


def main(data_path):
    """전체 특징 추출 파이프라인 실행"""
    pass  # TODO
