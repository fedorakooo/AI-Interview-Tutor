import asyncio

from src.agent.services.cv_analyzer import ICVAnalyzer
from src.domain.adapters.outbound.mongo import IMongoRepository
from src.domain.adapters.outbound.pdf_loader import IPDFLoader
from src.domain.adapters.outbound.s3 import IS3Client


class CVAnalyzeUseCase:
    def __init__(
        self,
        s3_client: IS3Client,
        cv_analyzer: ICVAnalyzer,
        pdf_loader: IPDFLoader,
        mongo_repository: IMongoRepository,
    ):
        self.s3_client = s3_client
        self.cv_analyzer = cv_analyzer
        self.pdf_loader = pdf_loader
        self.mongo_repository = mongo_repository

    async def __call__(self, url: str):
        pdf_bytes = await self.s3_client.get_file(url)

        extracted_text: str = await asyncio.to_thread(self.pdf_loader.load, pdf_bytes)

        analysis_result = await self.cv_analyzer.analyze(content=extracted_text)

        await self.mongo_repository.insert_one(analysis_result.model_dump(mode="json"))
