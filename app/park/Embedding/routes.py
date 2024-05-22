from flask import Blueprint, request, jsonify
from .algorithm import process_embedding, get_embeddings_by_category
import logging
from app.common.models import Item  # 올바른 경로로 Item을 임포트
import json
from scipy.spatial.distance import cosine

embedding_bp = Blueprint('embedding', __name__)

@embedding_bp.route('/embedding', methods=['POST'])
def embedding():
    try:
        logging.info("Embedding route called")  # 디버그 메시지 추가
        # JSON 데이터를 받아옴
        data = request.get_json()

        # 받은 데이터를 출력
        logging.info(f"Received data: {data}")

        # 데이터에서 id 값을 추출
        item_id = data.get('id')

        # 해당 ID로 category_embeddings 로직 호출
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            return jsonify({'status': 'fail', 'message': 'Item not found'}), 404

        category_id = item.category_id
        embeddings = get_embeddings_by_category(category_id)

        # 현재 아이템의 임베딩을 로드합니다
        current_embedding = json.loads(item.embedding)

        # 코사인 유사도 계산
        similarities = []
        for embedding in embeddings:
            other_embedding = json.loads(embedding['embedding'])
            similarity = 1 - cosine(current_embedding, other_embedding)
            similarities.append({
                'item_id': embedding['id'],
                'similarity': similarity
            })

        # 유사도를 기준으로 내림차순 정렬
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        # 상위 8개만 선택
        top_similarities = similarities[1:9]

        logging.info(f"Top 8 similar items: {top_similarities}")
        return jsonify({'status': 'success', 'data': top_similarities})
    except Exception as e:
        logging.error(f"Error in embedding route: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500
