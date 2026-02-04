from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.predictionLog import PredictionLogCreateSchema
from app.models.predictionLog import PredictionLog


async def create_prediction_log(
    db: AsyncSession,
    prediction_log : PredictionLogCreateSchema
) -> PredictionLog:
    
    log = PredictionLog(
        ticket_id=prediction_log.ticket_id,
        input_text=prediction_log.input_text,
        predicted_category_id=prediction_log.predicted_category_id,
        predicted_priority_id=prediction_log.predicted_priority_id,
        confidence_category=prediction_log.confidence_category,
        confidence_priority=prediction_log.confidence_priority,
        model_name=prediction_log.model_name,
    )

    db.add(log)
    await db.commit()
    await db.refresh(log)
    
    return log
