# prompt_manager.py

CATEGORIES = ["텍스트 생성", "이미지 생성", "페르소나", "코드 생성", "기타"]


def get_initial_data():
    """초기 프롬프트 데이터 3개를 리스트로 반환"""
    return [
        {
            "title": "블로그 글 작성 도우미",
            "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요.",
            "category": "텍스트 생성",
            "favorite": True,
        },
        {
            "title": "제품 썸네일 생성",
            "content": "다음 제품의 매력적인 썸네일 이미지를 생성해주세요. 배경은 깔끔하고 제품이 돋보이도록 해주세요.",
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "IT 컨설턴트 페르소나",
            "content": "당신은 15년 경력의 IT 컨설턴트입니다. 기술적인 질문에 대해 비전문가도 이해할 수 있도록 쉽게 설명해주세요.",
            "category": "페르소나",
            "favorite": False,
        },
    ]


def show_menu():
    """메뉴 출력"""
    print("\n=== 프롬프트 관리 프로그램 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록 보기")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def add_prompt(prompts):
    """새 프롬프트 추가"""
    pass  # TODO


def list_prompts(prompts):
    """프롬프트 목록 출력"""
    pass  # TODO


def filter_by_category(prompts):
    """카테고리별 필터링"""
    pass  # TODO


def search_prompts(prompts):
    """키워드로 프롬프트 검색"""
    pass  # TODO


def show_detail(prompts):
    """프롬프트 상세 정보 출력"""
    pass  # TODO


def manage_favorite(prompts):
    """즐겨찾기 토글 (추가/해제)"""
    pass  # TODO


def show_favorites(prompts):
    """즐겨찾기 프롬프트만 출력"""
    pass  # TODO


def main():
    prompts = get_initial_data()

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            list_prompts(prompts)
        elif choice == "3":
            filter_by_category(prompts)
        elif choice == "4":
            search_prompts(prompts)
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            manage_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
