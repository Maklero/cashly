import Image from 'next/image'

import Informer from '@/components/Informer/Informer'

import AddButton from '../../AddButton'
import ImportButton from '../../ImportButton'
import { StyledButtonContainer } from './EmptyInformer.styled'

export default function EmptyInformer() {
    return (
        <Informer
            bottomElement={
                <StyledButtonContainer>
                    <AddButton />
                    <ImportButton />
                </StyledButtonContainer>
            }
            illustration={<Image src="void.svg" alt="empty list" fill />}
            text={'Aktualnie lista wydatków jest pusta'}
        />
    )
}
